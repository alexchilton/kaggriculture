"""Drive the real interpreter and our sim with the same recorded tape; compare LIVE state.

**Why this exists rather than comparing against the replay JSON.** The recorded observation is not a
clean post-step snapshot, and two hours were spent mistaking its quirks for simulator bugs. Measured
directly (`kaggle_environments.make` + `env.toJSON()`, a controlled two-agent episode):

    t=22  shed {'WHEAT': 3}  inv [{}]          <- PICKUP decided here, not yet applied
    t=23  shed {}            inv [{'WHEAT': 3}] <- applied; still NOT dropped to the shed
    t=24  shed {'WHEAT': 3}  inv [{}]          <- the drop appears only on the next step

So `observation[t]` reflects `action[t]`, but is captured **before that step's `_end_of_day`**. Money
and seeds are post-action; shed, carried inventories and the animal/plant daily refresh are not. Any
comparison of those fields against the JSON reports a divergence on every single day boundary that is
purely an artifact of when the recorder looked.

This script sidesteps all of it: both engines are driven by the same actions and compared on their own
live state, so a difference here is real. That is the standard `kagg/sim/parity.py` gate applied to a
*recorded* script instead of a random one -- which matters, because CLAUDE.md's repeated lesson is that
a gate only tests what it exercises, and random scripts never reproduce a leader's opening.

    PYTHONPATH=. python3 -u scripts/tape_vs_reference.py 2>&1 | tee data/logs/tape_vs_reference.log
"""

import argparse
import json

import numpy as np

from kagg.search import executor as X
from kagg.sim.game import Actions, Game
from kagg.sim.market import ITEMS, PRODUCTS
from kagg.sim.town import SHOP_INDEX, SHOPS

TURNS_PER_DAY = 24


def _live_reference(steps, n_turns, seed, schedule=None):
    """Play the tape through `kaggle_environments` itself, snapshotting live state each step.

    `schedule` forces the reference's unlocked shops to the recorded ones. **This is not a shortcut.**
    `_end_of_day` builds one `random.Random` and hands it to `_spawn_weeds` *before* calling
    `rng.choice(sorted(remaining))`, and `_spawn_weeds` draws once per empty tile -- so which shop
    unlocks depends on both players' board occupancy, not on the seed alone. Recovering it by brute
    force does not work (seed 13981 predicts SMOOTHIE_SHOP by the formula and the live env produces
    FARMERS_MARKET), and episodes record `configuration.seed: null` anyway.

    CLAUDE.md already classes the unlock order as a deliberate deviation to be neutralised in the gate
    rather than reproduced. Imposing the same schedule on both engines is what makes everything else --
    market settlement, tiles, money -- an apples-to-apples comparison.
    """
    from kaggle_environments import make

    plan = [[steps[t][seat].get("action") for seat in range(2)] for t in range(len(steps))]
    cursor = {"t": 0}

    def make_agent(seat):
        def agent(obs, config=None):
            t = min(cursor["t"], len(plan) - 1)
            act = plan[t][seat]
            return act if isinstance(act, dict) else {"farmer": ["PASS"], "hands": [], "market": []}
        return agent

    # Weeds off on BOTH sides. Our sim cannot reproduce the reference's weed RNG stream -- CLAUDE.md
    # records that as a deliberate, neutralised deviation -- so leaving them on would compare two
    # different games and bury any real divergence under noise.
    env = make("kaggriculture",
               configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    # **`env.info["seed"]`, not `configuration["seed"]`.** `_end_of_day` reads
    # `env.info.get("seed", 0)` to key the shop-unlock RNG (`reference/kaggriculture.py:838`), so a
    # seed passed through `configuration` is silently ignored and every run unlocks the seed-0
    # sequence. Episodes record `configuration.seed: null`, so the seat's real seed is recovered by
    # brute force against its observed unlock order -- 13981 for episode 89873723.
    env.info = dict(env.info or {})
    env.info["seed"] = seed
    env.reset(2)
    trace = []
    for t in range(n_turns):
        cursor["t"] = t
        env.step([make_agent(0)(env.state[0].observation),
                  make_agent(1)(env.state[1].observation)])
        obs0 = env.state[0].observation
        if schedule is not None:
            day = (t + 1) // TURNS_PER_DAY
            want = [SHOPS[i] for d, i in sorted(schedule.items()) if d <= day]
            obs0.town["unlocked_shops"] = list(want)
        privates = [s.observation.private for s in env.state]
        trace.append({
            "money": [float(obs0.farms[i]["money"]) for i in range(2)],
            "shed": [{k: int(v) for k, v in (privates[i].get("shed") or {}).items() if v}
                     for i in range(2)],
            "shops": sorted((obs0.town or {}).get("unlocked_shops", [])),
            "inv": dict(obs0.market["inventory"]),
        })
        if env.done:
            break
    return trace


def _live_sim(steps, n_turns, schedule, seed):
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("rtd", "scripts/replay_tape_day.py")
    rtd = importlib.util.module_from_spec(spec)
    sys.modules["rtd"] = rtd
    spec.loader.exec_module(rtd)

    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(seed), unlock_schedule=schedule)
    trace = []
    for t in range(n_turns):
        actions = Actions(1)
        for seat in range(2):
            act = steps[t][seat].get("action")
            if not isinstance(act, dict):
                continue
            units = [act.get("farmer")] + list(act.get("hands") or [])
            for slot, entry in enumerate(units[: X.MAX_EXEC_UNITS]):
                rtd.write_unit(actions, seat, slot, entry)
            rtd.write_market(actions, seat, act.get("market"))
        game.step(actions)
        trace.append({
            "money": [float(game.farms[i].money[0]) for i in range(2)],
            "shed": [{ITEMS[i]: int(v) for i, v in enumerate(game.farms[s].shed[0]) if v}
                     for s in range(2)],
            "inv": {p: int(game.inventory[0, i]) for i, p in enumerate(PRODUCTS)},
            "shops": sorted(SHOPS[i] for i in range(len(SHOPS))
                            if bool(game.unlocked_shops[0, i])),
        })
    return trace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/episodes/89873723.json")
    ap.add_argument("--turns", type=int, default=120)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    steps = json.loads(open(a.episode).read())["steps"]
    n = min(a.turns, len(steps))

    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location("rtd", "scripts/replay_tape_day.py")
    rtd = importlib.util.module_from_spec(spec)
    sys.modules["rtd"] = rtd
    spec.loader.exec_module(rtd)
    schedule = rtd.unlock_schedule(steps)

    ref = _live_reference(steps, n, a.seed, schedule=schedule)
    sim = _live_sim(steps, n, schedule, a.seed)

    print(f"{a.episode}: same tape into both engines, live state compared, {n} turns\n")
    print(f"{'turn':>5} {'d':>2} {'h':>2} | {'ref $':>10} {'sim $':>10} {'delta':>9} | shed")
    print("=" * 92)
    first = None
    for t in range(min(len(ref), len(sim))):
        dm = sim[t]["money"][0] - ref[t]["money"][0]
        ds = sim[t]["shed"][0] != ref[t]["shed"][0]
        di = {k: (sim[t]["inv"][k], ref[t]["inv"][k])
              for k in ref[t]["inv"] if sim[t]["inv"].get(k) != ref[t]["inv"][k]}
        # Compared one step later: `_end_of_day` appends the new shop while finishing step 71, and we
        # apply it as day 3 begins at step 72. Both are live before step 72's market -- which is the
        # only thing that consumes it -- so the difference is where the label lands, not behaviour.
        nxt = min(t + 1, len(sim) - 1)
        dshop = sim[nxt].get("shops") != ref[t].get("shops")
        if abs(dm) > 0.5 or ds or di or dshop:
            if first is None:
                first = t
            if t < (first or 0) + 6:
                print(f"{t:>5} {t // TURNS_PER_DAY:>2} {t % TURNS_PER_DAY:>2} | "
                      f"{ref[t]['money'][0]:>10,.0f} {sim[t]['money'][0]:>10,.0f} {dm:>+9,.0f} | "
                      f"{'SHED DIFFERS' if ds else ''}")
                if ds:
                    print(f"        ref shed {ref[t]['shed'][0]}")
                    print(f"        sim shed {sim[t]['shed'][0]}")
                if di:
                    print(f"        market inventory (sim, ref): {di}")
                if dshop:
                    print(f"        shops sim={sim[t].get('shops')} ref={ref[t].get('shops')}")
    print("=" * 92)
    print(f"first REAL divergence (live vs live): {first}")
    if first is None:
        print(f"our sim matches the reference interpreter exactly over {n} turns of the winner's tape")


if __name__ == "__main__":
    raise SystemExit(main())
