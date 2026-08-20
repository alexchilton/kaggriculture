"""Play one season and look for the failure modes that a win rate hides.

Written after a market-code variant kept 4/0 while losing twelve animals on one board. A bank total
cannot show that, and neither can a win: the herd is an asset that pays out over the remaining days,
so losing it late costs little on the scoreboard and a great deal on the next board along.

Four things, all read off the live observation rather than inferred:

  herd        animals alive at dawn. A FALL is an escape -- `consecutive_unfed >= 2` deletes the
              animal outright (`kaggriculture.py:786`), so this is the irreversible one.
  shed        slots used of `shedCapacity`. Near the cap means the harvest has nowhere to land and a
              night's production is binned at the rollover.
  held        units sitting in HANDS at dusk. The market reads the shed and nothing else, so this is
              produce that was made and never sellable that day.
  hi-value    of that, the units the price table actually pays for -- milk, wool, melon, strawberry.
              Wheat sitting in a hand is feed; milk sitting in a hand is money that never arrived.
"""
import collections
import importlib
import json
import os
import pathlib
import sys

MOD = os.environ.get("MOD", "schedule_agent")
SEED = int(os.environ.get("SEED", "13"))
HI = ("MILK", "WOOL", "MELON", "STRAWBERRY")
ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    sys.path.insert(0, str(ROOT))
    SA = importlib.import_module("kagg.search." + MOD)
    from kaggle_environments import make

    from kagg.arena.tape import build_tape_agent
    sched = {int(k): v for k, v in json.loads(
        (ROOT / "data/seed_scripts/top_guys/90976060/schedule.json").read_text()).items()}
    thin = {d: {k: v for k, v in r.items()
                if k not in ("plant_tiles", "build_tiles", "land_turns", "orders")}
            for d, r in sched.items()}
    ours = SA.make_agent(thin, 0, router=True)
    rival = build_tape_agent(str(ROOT / "data/seed_scripts/top_guys/90976060.json"), 0)
    env = make("kaggriculture", configuration={"seed": SEED}, debug=False)
    env.reset(2)
    cap = int((env.configuration or {}).get("shedCapacity", 100) or 100)

    print(f"{MOD}  seed {SEED}  shedCapacity {cap}")
    print(" day  herd  shed  hi_shed  held  hi_held  bank      note")
    prev_herd = None
    for t in range(24 * 30):
        if env.done:
            break
        o0 = env.state[0].observation
        if t % 24 == 23:                                   # dusk: after the day's work
            f = o0["farms"][0]
            priv = o0.get("private") or {}
            shed = collections.Counter(priv.get("shed") or {})
            held = collections.Counter()
            for iv in (priv.get("inventories") or []):
                held.update(iv or {})
            herd = sum(1 for r in f["tiles"] for c in r
                       if isinstance(c, dict) and "animal" in c)
            note = []
            if prev_herd is not None and herd < prev_herd:
                note.append(f"LOST {prev_herd - herd} ANIMAL(S)")
            if sum(shed.values()) >= cap - 5:
                note.append("SHED NEAR CAP")
            hi_held = sum(held[p] for p in HI)
            if hi_held >= 10:
                note.append(f"{hi_held} HI-VALUE STRANDED IN HANDS")
            print(" %3d  %4d  %4d  %7d  %4d  %7d  %8.0f  %s"
                  % (t // 24, herd, sum(shed.values()), sum(shed[p] for p in HI),
                     sum(held.values()), hi_held, float(f["money"]), ", ".join(note)))
            prev_herd = herd
        a0 = ours(o0)
        a1 = rival(env.state[1].observation)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])


if __name__ == "__main__":
    main()
